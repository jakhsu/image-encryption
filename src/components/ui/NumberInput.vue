<script setup>
import { ref } from 'vue'
const props = defineProps([
    'modelValue',
    'error',
    'label',
    'inputName',
    'inputType',
])
const emits = defineEmits(['update:modelValue'])
</script>

<template>
    <div>
        <label
            :for="props.inputName"
            class="block text-sm font-medium leading-6 text-gray-900"
            >{{ props.label }}</label
        >
        <div class="relative mt-2 rounded-md shadow-sm">
            <input
                :type="props.inputType"
                :name="props.inputName"
                :id="props.inputName"
                class="block w-full rounded-md border-0 py-1.5 pr-10 text-blue-900 ring-1 ring-inset placeholder:text-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6"
                placeholder="3"
                aria-invalid="true"
                aria-describedby="input-error"
                :class="{ 'ring-red-300': props.error }"
                :value="props.modelValue"
                @input="$emit('update:modelValue', $event.target.value)"
                @blur="$emit('update:modelValue', $event.target.value)"
            />
            <div
                class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3"
            ></div>
        </div>
        <p
            v-if="props.error"
            class="mt-2 text-sm text-red-600"
            id="input-error"
        >
            請輸入 1 到 250 之間的數字.
        </p>
    </div>
</template>
