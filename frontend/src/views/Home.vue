<script setup lang="ts">
import { useRouter } from 'vue-router';
import { publicLayout } from '@/components/layouts';
import {
    HeroSection,
    DescriptionCard,
    FeatureCard,
    FeaturesGrid,
    CallToActionCard,
} from '@/components/ui';

const router = useRouter();

const features = [
    {
        icon: '📊',
        title: 'Data-Driven',
        description:
            'Uses machine learning to analyze multiple factors including fuel prices, exchange rates, and regional data.',
    },
    {
        icon: '🎯',
        title: 'Accurate Predictions',
        description:
            'Get precise price predictions based on comprehensive market analysis and historical trends.',
    },
    {
        icon: '🌍',
        title: 'Regional Analysis',
        description:
            'Predictions tailored to different regions with specific market characteristics and local conditions.',
    },
    {
        icon: '⚡',
        title: 'Real-Time Results',
        description:
            'Get instant predictions by entering your parameters. Fast and reliable results every time.',
    },
];

const handlePredictionClick = () => {
    router.push('/predict');
};
</script>

<template>
    <div>
        <publicLayout pageTitle="Home">
            <div class="home-container">
                <!-- Hero Section -->
                <HeroSection
                    title="Rice Price Prediction"
                    subtitle="Predict rice market prices using machine learning"
                />

                <!-- Description Section -->
                <DescriptionCard
                    title="About This App"
                    content="Welcome to the Rice Price Prediction application. This tool helps you predict rice market prices based on various economic and regional factors. By analyzing historical data and current market conditions, our machine learning model provides accurate price predictions to assist in decision-making."
                />

                <!-- Features Section -->
                <FeaturesGrid title="Key Features">
                    <FeatureCard
                        v-for="(feature, index) in features"
                        :key="index"
                        :icon="feature.icon"
                        :title="feature.title"
                        :description="feature.description"
                    />
                </FeaturesGrid>

                <!-- CTA Section -->
                <CallToActionCard
                    title="Ready to Get Started?"
                    description="Use our prediction tool to forecast rice prices for your region and commodity type."
                    buttonText="Go to Prediction"
                    @click="handlePredictionClick"
                />
            </div>
        </publicLayout>
    </div>
</template>

<style scoped>
.home-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}
</style>
