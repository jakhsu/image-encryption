<script setup>
import { ref } from 'vue'
const props = defineProps(['text'])
const emit = defineEmits(['click'])
</script>
<template>
    <button
        type="button"
        @click="emit('click')"
        class="rounded bg-indigo-600 px-2 py-1 text-xs font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
    >
        {{ props.text }}
    </button>
</template>
