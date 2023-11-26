<script setup>
import Button from './ui/Button.vue'

const props = defineProps(['items'])
const emit = defineEmits(['click'])
</script>

<template>
    <div class="flex flex-row justify-center space-x-3">
        <p>選擇操作：</p>
        <template v-for="item in props.items">
            <Button @click="emit('click', item)" :text="item" />
        </template>
    </div>
</template>
