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
    background-color: #f0f0f0;
    padding: 3rem 2rem;
    border-radius: 8px;
}

.cta-card h2 {
    color: #333;
    margin-top: 0;
    margin-bottom: 0.5rem;
}

.cta-card p {
    color: #666;
    margin-bottom: 1.5rem;
}
</style>
