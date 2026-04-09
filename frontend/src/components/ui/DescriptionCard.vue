<template>
    <section class="description">
        <div class="description-card">
            <h2>{{ title }}</h2>
            <p>{{ content }}</p>
        </div>
    </section>
</template>

<script setup lang="ts">
defineProps<{
    title: string;
    content: string;
}>();
</script>

<style scoped>
.description {
    margin-bottom: 3rem;
}

.description-card {
    background-color: var(--color-bg-light);
    padding: 2rem;
    border-radius: 8px;
    border-left: 4px solid var(--color-accent);
}

.description-card h2 {
    margin-top: 0;
    color: var(--color-text-primary);
}

.description-card p {
    color: var(--color-text-secondary);
    line-height: 1.6;
    margin: 0;
}
</style>
