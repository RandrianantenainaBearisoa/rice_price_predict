<template>
    <section class="features">
        <h2>{{ title }}</h2>
        <div class="features-grid">
            <slot></slot>
        </div>
    </section>
</template>

<script setup lang="ts">
defineProps<{
    title: string;
}>();
</script>

<style scoped>
.features {
    margin-bottom: 3rem;
}

.features h2 {
    text-align: center;
    color: var(--color-text-primary);
    margin-bottom: 2rem;
    font-size: 1.8rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: 1fr;
    }
}
</style>
