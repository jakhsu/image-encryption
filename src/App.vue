<script setup>
import { computed, ref } from 'vue'
import ImageUpload from './components/ImageUpload.vue'
import PrepareList from './components/PrepareList.vue'
import KeysInputs from './components/KeysInputs.vue'
import NumberInput from './components/ui/NumberInput.vue'
import Button from './components/ui/Button.vue'
import { useGlobalStore } from './store/globalStore.js'
import ProcessedImages from './components/ProcessedImages.vue'
import Dropdown from './components/Dropdown.vue'
const showImageUpload = ref(false)
const showKeysInputs = ref(false)
const showSubmit = ref(false)

const mode = ref('')
const colorMode = ref('')
const globalStore = useGlobalStore()
const startProcess = () => {
    showImageUpload.value = true
}
const handleUploadImageDone = (done) => {
    if (done) {
        showKeysInputs.value = true
    }
}
const handleKeyInputsDone = (done) => {
    if (done) {
        showSubmit.value = true
    }
}

const submitText = computed(
    () =>
        globalStore.processingConfig.mode +
        globalStore.processingConfig.colorMode
)

const handleSubmit = async () => {
    if (
        globalStore.processingConfig.mode === '加密' &&
        globalStore.processingConfig.colorMode === '彩圖'
    ) {
        const images = globalStore.originalImages
        const keys = globalStore.userKeys
        const name = globalStore.originalImages[0].name
        const requestBody = {
            images: images.map((image, index) => ({
                name: `image${index + 1}`,
                data: image.image,
            })),
            keys: keys.map((key, index) => ({
                value: key.value,
            })),
            name: name,
        }

        fetch('http://localhost:3000/encrypt/color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        })
            .then(async (response) => {
                console.log(response)
                if (!response.ok) {
                    if (response.status === 400) {
                        alert(`加密失敗: 重複金鑰`)
                    } else {
                        alert('加密失敗: 伺服器錯誤')
                    }
                }
                return response.json()
            })
            .then((data) => {
                const processedImages = data.result.map((image) => ({
                    user: image.name,
                    image: `data:image/png;base64,${image.data}`,
                }))
                globalStore.setProcessedImages(processedImages)
            })
            .catch((error) => {
                console.error('Error:', error)
            })
    } else if (globalStore.processingConfig.mode === '解密') {
        const images = globalStore.originalImages
        const keys = globalStore.userKeys

        const requestBody = {
            images: images.map((image, index) => ({
                name: `image${index + 1}`,
                data: image.image,
            })),
            keys: keys.map((key, index) => ({
                name: `key${index + 1}`,
                value: key.value,
            })),
        }

        fetch('http://localhost:3000/decrypt/color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        })
            .then((response) => {
                if (!response.ok) {
                    if (response.status === 400) {
                        alert(`解密失敗: 重複金鑰`)
                    } else {
                        alert('解密失敗: 伺服器錯誤')
                    }
                }
                return response.json() // Parse the response as JSON
            })
            .then((data) => {
                const processedImages = data.result.map((image) => ({
                    user: image.name,
                    image: `data:image/png;base64,${image.data}`,
                }))
                globalStore.setProcessedImages(processedImages)
            })
            .catch((error) => {
                console.error('Error:', error)
            })
    }
}

const handleDeleteAllKeys = async () => {
    try {
        const response = await fetch('http://localhost:3000/delete/keys', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                // Add any additional headers if needed
            },
        })

        if (response.ok) {
            const data = await response.json()
            alert(data.message)
        } else {
            // Handle errors if the request was not successful
            console.error(`Error: ${response.status} - ${response.statusText}`)
            alert(
                'Failed to delete keys. Please check the console for details.'
            )
        }
    } catch (error) {
        console.error('Error:', error)
        alert('An error occurred while deleting keys.')
    }
}
</script>
<template>
    <div class="flex flex-col space-y-4 text-center">
        <h1 class="text-3xl">圖像加密和解密</h1>
        <div class="fixed right-0 top-0">
            <Dropdown @deleteAllKeys="handleDeleteAllKeys" />
        </div>
        <PrepareList @done="startProcess" />
        <ImageUpload
            v-if="showImageUpload"
            :config="{ mode, colorMode }"
            @uploadImageDone="handleUploadImageDone"
            @done="handleKeyInputsDone"
        />
        <KeysInputs
            v-if="
                showKeysInputs && globalStore.processingConfig.mode === '加密'
            "
            @done="handleKeyInputsDone"
        />
        <div class="flex justify-center">
            <Button
                class="w-fit"
                v-if="showSubmit"
                :text="submitText"
                @click="handleSubmit"
            />
        </div>
        <ProcessedImages />
    </div>
</template>
