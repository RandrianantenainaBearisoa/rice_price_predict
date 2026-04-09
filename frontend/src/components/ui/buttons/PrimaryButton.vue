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
    background-color: var(--color-accent);
    color: var(--color-text-white);
    border: var(--color-accent) solid 1px;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s;
}

.primary-button:hover:not(:disabled) {
    background-color: var(--background-color-00);
    border-color: var(--color-accent-dark);
    color: var(--color-text-dark);
}

.primary-button:disabled {
    background-color: var(--color-disabled);
    cursor: not-allowed;
}
</style>
