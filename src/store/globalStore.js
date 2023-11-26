import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGlobalStore = defineStore('global', () => {
    const originalImages = ref([])
    const processedImages = ref([])
    const userKeys = ref([])
    const processingConfig = ref({
        mode: null,
        colorMode: null,
    })

    const setOriginalImages = (images) => {
        originalImages.value = images
    }

    const setProcessedImages = (images) => {
        processedImages.value = images
    }

    const setKeys = (keys) => {
        userKeys.value = keys
    }

    const setProcessingConfig = (config) => {
        processingConfig.value = config
    }

    return {
        originalImages,
        processedImages,
        userKeys,
        processingConfig,
        setOriginalImages,
        setProcessedImages,
        setKeys,
        setProcessingConfig,
    }
})
