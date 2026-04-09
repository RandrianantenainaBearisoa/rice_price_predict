<template>
    <button :type="type" :disabled="disabled" class="primary-button" @click="$emit('click')">
        {{ text }}
    </button>
</template>

<script setup lang="ts">
defineProps<{
    text: string;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
}>();

defineEmits<{
    click: [];
}>();
</script>

<style scoped>
.primary-button {
    width: 100%;
    padding: 0.75rem;
    background-color: var(--background-color-03);
    border: var(--background-color-00) solid 1px;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s;
}

.primary-button:hover:not(:disabled) {
    background-color: var(--background-color-00);
    color: var(--font-color-00);
    border: var(--font-color-00) solid 1px;
}

.primary-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>
