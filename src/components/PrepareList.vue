<script setup>
import { ref } from 'vue'
import Button from './ui/Button.vue'
import PrepareListItem from './PrepareListItem.vue'
import { useGlobalStore } from '../store/globalStore.js'

const globalStore = useGlobalStore()
const emits = defineEmits(['done'])
const step = ref(1)

const step1Items = ['加密', '解密']
const step2Items = ['彩圖', '灰階圖']

const config = ref({
    mode: '',
    colorMode: '',
})

const handleItemClick = (key) => {
    if (key === '解密') {
        config.value.mode = '解密'
        globalStore.setProcessingConfig(config.value)
        emits('done')
    } else if (key === '加密') {
        config.value.mode = '加密'
        globalStore.setProcessingConfig(config.value)
        step.value = 2
    } else if (key === '彩圖') {
        config.value.colorMode = '彩圖'
        globalStore.setProcessingConfig(config.value)
        emits('done')
    } else if (key === '灰階圖') {
        config.value.colorMode = '灰階圖'
        globalStore.setProcessingConfig(config.value)

        emits('done')
    }
}
</script>
<template>
    <div>
        <PrepareListItem
            v-show="step === 1"
            :items="['加密', '解密']"
            @click="handleItemClick"
        />
        <PrepareListItem
            v-show="step === 2"
            :items="['彩圖', '灰階圖']"
            @click="handleItemClick"
        />
    </div>
</template>
