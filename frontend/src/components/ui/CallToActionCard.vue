<template>
    <section class="cta">
        <div class="cta-card">
            <h2>{{ title }}</h2>
            <p>{{ description }}</p>
            <PrimaryButton :text="buttonText" @click="$emit('click')" />
        </div>
    </section>
</template>

<script setup lang="ts">
import PrimaryButton from './buttons/PrimaryButton.vue';

defineProps<{
    title: string;
    description: string;
    buttonText: string;
}>();

defineEmits<{
    click: [];
}>();
</script>

<style scoped>
.cta {
    text-align: center;
    margin-top: 3rem;
}

.cta-card {
    background-color: var(--color-bg-very-light);
    padding: 3rem 2rem;
    border-radius: 8px;
}

.cta-card h2 {
    color: var(--color-text-primary);
    margin-top: 0;
    margin-bottom: 0.5rem;
}

.cta-card p {
    color: var(--color-text-secondary);
    margin-bottom: 1.5rem;
}
</style>
