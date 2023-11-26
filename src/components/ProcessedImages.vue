<script setup>
import { useGlobalStore } from '../store/globalStore'

const globalStore = useGlobalStore()

let userIndexMap = {}
const getProcessedImageUserName = (index) => {
    const userId = userIndexMap[index]
    return userId !== undefined ? `User ${userId + 1}` : false
}

const updateIndexMap = () => {
    userIndexMap = {}
    globalStore.userKeys.forEach((key, index) => {
        userIndexMap[key.id] = index
    })
}

const getUserKey = (index) => {
    const userKey = globalStore.userKeys[index + 1]
    return userKey ? `User ${userKey.id}` : `User ${index + 1}`
}
</script>

<template>
    <div>
        <div class="flex flex-wrap justify-center">
            <div
                class="m-2 w-[30%] p-2"
                v-for="(image, index) in globalStore.processedImages"
                :key="index"
            >
                <h1 class="text-2xl">使用者 {{ index + 1 }}</h1>
                <img
                    :src="image.image"
                    alt="processed-image"
                    class="object-fill"
                />
            </div>
        </div>
    </div>
</template>
