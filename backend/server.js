const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const { spawn } = require('child_process')
const multer = require('multer') // 中介軟體，用於處理檔案上傳
const cors = require('cors')
const fs = require('fs')
const path = require('path')

app.use(cors())
app.use(express.json({ limit: '100mb' }))

// 提供 HTML 檔案
app.use(express.static('public'))

// 解析 URL 編碼的主體
app.use(bodyParser.urlencoded({ extended: true }))

// 設定 multer 用於處理檔案上傳
const storage = multer.memoryStorage() // 將檔案存儲在記憶體中
const upload = multer({ storage: storage })

// 刪除目錄中所有先前的檔案的函式
function deletePreviousFiles(directory) {
    try {
        const files = fs.readdirSync(directory)

        files.forEach((file) => {
            const filePath = path.join(directory, file)
            fs.unlinkSync(filePath)
        })

        console.log('先前的檔案刪除成功。')
    } catch (error) {
        console.error('刪除先前檔案時發生錯誤：', error)
    }
}

function hasDuplicateKeys(existingKeys, newKeys) {
    const uniqueKeys = new Set([...existingKeys, ...newKeys])
    return newKeys.length + existingKeys.length !== uniqueKeys.size
}

// 定義處理具有檔案上傳的表單提交的路由
app.post('/encrypt/color', upload.array('images', 1), (req, res) => {
    try {
        const keys = req.body.keys.map((key) => key.value)
        const images = req.body.images.map((image) => image.data)
        const imageName = req.body.name
        const keysFilePath = path.join(__dirname, 'keys', `${imageName}.txt`)
        const numberOfKeysToUse = keys.length

        // Read existing keys from the file
        let existingKeys = []
        if (fs.existsSync(keysFilePath)) {
            existingKeys = fs
                .readFileSync(keysFilePath, 'utf-8')
                .split('\n')
                .map(Number)
        }

        // Check for duplicate keys
        if (hasDuplicateKeys(existingKeys, keys)) {
            // Return a status indicating that there are duplicate keys
            return res.status(400).json({
                error: `檔案 ${imageName} 已有重複金鑰`,
            })
        }

        fs.appendFileSync(keysFilePath, `${keys.join('\n')}\n`)

        const selectedImgDir = path.join(__dirname, 'color_selected')
        deletePreviousFiles(selectedImgDir)

        images.forEach((image, index) => {
            const base64Data = image.replace(/^data:image\/\w+;base64,/, '')
            const buffer = Buffer.from(base64Data, 'base64')
            fs.writeFileSync(
                path.join(selectedImgDir, `${imageName}.png`),
                buffer
            )
        })

        const pythonScriptPath = path.join(__dirname, 'colorEncrypt.py')

        // Call the Python script
        const pythonProcess = spawn('python3', [
            pythonScriptPath,
            numberOfKeysToUse,
        ])

        // Handle the end of the Python script execution
        pythonProcess.on('close', (code) => {
            console.log(`Python script exited with code ${code}`)

            // Read the encrypted images from the "color_encrypted" folder
            const encryptedImagesDir = path.join(__dirname, 'color_encrypted')
            const encryptedImages = []

            fs.readdirSync(encryptedImagesDir).forEach((file) => {
                const filePath = path.join(encryptedImagesDir, file)
                const imageBuffer = fs.readFileSync(filePath)
                const base64Image = imageBuffer.toString('base64')
                encryptedImages.push({ name: file, data: base64Image })
            })

            // You can now send the result and encrypted images back to the frontend
            res.status(200).json({ result: encryptedImages })
        })

        pythonProcess.stdout.on('data', (data) => {
            console.log(`Python script stdout: ${data}`)
        })

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python script stderr: ${data}`)
        })
    } catch (error) {
        console.error('錯誤：', error)
        res.status(500).send('內部伺服器錯誤')
    }
})
app.post('/decrypt/color', upload.array('images', 3), (req, res) => {
    try {
        const keys = req.body.keys.map((key) => key.value)
        const images = req.body.images.map((image) => image.data)

        // Now you have keys and images as arrays

        // Save the keys to a local file
        const keysFilePath = path.join(__dirname, 'keys', 'keys.txt')
        fs.writeFileSync(keysFilePath, keys.join('\n'))

        // Save the images to a local folder
        const selectedImgDir = path.join(__dirname, 'color_selected')
        deletePreviousFiles(selectedImgDir)

        images.forEach((image, index) => {
            const base64Data = image.replace(/^data:image\/\w+;base64,/, '')
            const buffer = Buffer.from(base64Data, 'base64')
            fs.writeFileSync(
                path.join(selectedImgDir, `colorImg${index + 1}.png`),
                buffer
            )
        })

        const pythonScriptPath = path.join(__dirname, 'colorDecrypt.py')

        // Call the Python script
        const pythonProcess = spawn('python3', [pythonScriptPath])

        // Handle the end of the Python script execution
        pythonProcess.on('close', (code) => {
            console.log(`Python script exited with code ${code}`)

            // Read the decrypted images from the "color_decrypted" folder
            const decryptedImagesDir = path.join(__dirname, 'color_decrypted')
            const decryptedImages = []

            fs.readdirSync(decryptedImagesDir).forEach((file) => {
                const filePath = path.join(decryptedImagesDir, file)
                const imageBuffer = fs.readFileSync(filePath)
                const base64Image = imageBuffer.toString('base64')
                decryptedImages.push({ name: file, data: base64Image })
            })

            // You can now send the result and decrypted images back to the frontend
            res.status(200).json({ result: decryptedImages })
        })
    } catch (error) {
        console.error('錯誤：', error)
        res.status(500).send('內部伺服器錯誤')
    }
})
const port = 3000
app.listen(port, () => {
    console.log(`伺服器正在運行，網址：http://localhost:${port}`)
})
