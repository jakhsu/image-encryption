<script setup>
import { useFileDialog } from '@vueuse/core'
import Button from './ui/Button.vue'
import { computed, ref, watch } from 'vue'
import { useGlobalStore } from '../store/globalStore'
import NumberInput from './ui/NumberInput.vue'

const props = defineProps({ config: Object })
const emits = defineEmits(['uploadImageDone', 'done'])
const globalStore = useGlobalStore()

const { files, open, reset, onChange } = useFileDialog({
    accept: 'image/*',
})

const handleSelects = async (fileList) => {
    const images = []

    for (const file of fileList) {
        if (!file.type.match('image.*')) {
            continue
        }

        const image = await loadImage(file)
        images.push({
            image: image,
            name: file.name,
        })
    }

    // Update the global store with the new images
    globalStore.setOriginalImages(images)
    startProcess()
}

const loadImage = (file) => {
    return new Promise((resolve) => {
        const reader = new FileReader()

        reader.onload = function (e) {
            resolve(e.target.result)
        }

        reader.readAsDataURL(file)
    })
}

onChange((files) => {
    const fileList = Array.from(event.target.files)
    if (props.config.mode === '加密' && props.config.colorMode === '彩圖') {
        if (fileList.length === 1) {
            handleSelects(fileList)
        } else {
            alert('加密彩圖只能選擇一張圖片')
        }
    } else if (
        props.config.mode === '加密' &&
        props.config.colorMode === '灰階圖'
    ) {
        if (fileList.length === 3) {
            handleSelects(fileList)
        } else {
            alert('加密灰階圖需要選擇三張圖片')
        }
    } else if (props.config.mode === '解密') {
        if (fileList.length === 3) {
            handleSelects(fileList)
        } else {
            alert('解密需要選擇三張圖片')
        }
    } else {
        handleSelects(fileList)
    }
    emits('uploadImageDone', true)
})

const userKeyValue = (index) => {
    return globalStore.userKeys[index]?.value ?? 0
}

const keyInputs = ref([])
const numOfKeyInputs = ref(0)

const startProcess = () => {
    numOfKeyInputs.value = globalStore.originalImages.length
    keyInputs.value = Array.from(
        { length: numOfKeyInputs.value },
        (_, index) => ({
            id: index,
            value: Number(0),
        })
    )
}

const updateUserKeyValue = (index, newValue) => {
    if (globalStore.processingConfig.mode === '解密') {
        // Make sure globalStore.userKeys[index] exists before updating
        if (!globalStore.userKeys[index]) {
            globalStore.userKeys[index] = { id: index + 1, value: 0 }
        }

        // Update the value
        globalStore.userKeys[index].value = newValue
    }
}

watch(
    keyInputs,
    (newKeys) => {
        globalStore.setKeys(newKeys)
        emits('done', true)
    },
    { deep: true }
)
</script>
<template>
    <div>
        <Button text="上傳圖片" @click="open"></Button>
        <div class="flex flex-wrap justify-center">
            <div
                class="m-2 w-[30%] p-2"
                v-for="(image, index) in globalStore.originalImages"
                :key="index"
            >
                <img
                    :src="image.image"
                    alt="uploaded-image"
                    class="object-fill"
                />
                <div
                    v-if="
                        globalStore.processingConfig.mode === '解密' &&
                        keyInputs[index]
                    "
                >
                    <NumberInput
                        :inputType="'password'"
                        v-model="keyInputs[index].value"
                        :id="`keyInput${index}`"
                        :label="`使用者 ${index + 1}`"
                        :inputName="`keyInput ${index + 1}`"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
