<template>
    <section class="hero">
        <div class="hero-content">
            <h1 class="hero-title">{{ title }}</h1>
            <p class="hero-subtitle">{{ subtitle }}</p>
        </div>
    </section>
</template>

<script setup lang="ts">
defineProps<{
    title: string;
    subtitle: string;
}>();
</script>

<style scoped>
.hero {
    text-align: center;
    padding: 4rem 2rem;
    border-radius: 8px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-bottom: 3rem;
}

.hero-title {
    font-size: 2.5rem;
    margin: 0 0 1rem;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 1.25rem;
    margin: 0;
    opacity: 0.9;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }

    .hero-subtitle {
        font-size: 1rem;
    }

    .hero {
        padding: 2rem;
    }
}
</style>
