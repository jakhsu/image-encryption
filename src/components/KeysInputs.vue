<script setup>
import { ref, watch } from 'vue'
import NumberInput from './ui/NumberInput.vue'
import Button from './ui/Button.vue'
import { useGlobalStore } from '../store/globalStore.js'

const shareValue = ref(0)
const emits = defineEmits(['done'])
const globalStore = useGlobalStore()

const startProcess = () => {
    numOfKeyInputs.value = shareValue.value
    keyInputs.value = Array.from(
        { length: numOfKeyInputs.value },
        (_, index) => ({
            id: index,
            value: Number(0),
        })
    )
}

const validateInput = (inputValue) => {
    return inputValue < 1 || inputValue > 250
}

const numOfKeyInputs = ref(0)
const keyInputs = ref([])

const removeKeyInput = (id) => {
    const indexToRemove = keyInputs.value.findIndex((input) => input.id === id)
    if (indexToRemove !== -1) {
        keyInputs.value.splice(indexToRemove, 1)
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
    <div class="flex justify-center text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
            <div class="flex w-fit flex-col justify-center space-y-4">
                <NumberInput
                    :inputType="'number'"
                    v-model="shareValue"
                    label="輸入分享份數"
                    inputName="share"
                    @keydown.enter="startProcess"
                    :error="validateInput(shareValue)"
                />
                <Button text="確認分享份數" @click="startProcess" />
            </div>
            <div
                class="flex w-screen flex-row flex-wrap justify-center space-x-2"
            >
                <div
                    class="flex w-[20%] flex-row space-x-3"
                    v-for="input in keyInputs"
                    :key="input.id"
                >
                    <NumberInput
                        :inputType="'password'"
                        v-model="input.value"
                        :label="`使用者 ${input.id + 1}`"
                        :inputName="`keyInput${input.id + 1}`"
                    />
                    <div
                        class="flex cursor-pointer items-end justify-center text-3xl"
                        @click="removeKeyInput(input.id)"
                    >
                        ❌
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
