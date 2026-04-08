import { createRouter, createWebHistory } from "vue-router";
import { type RouteRecordRaw} from "vue-router";
import { home, predictionView } from "@/views";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "home",
        component: home
    },
    {
        path: "/predict",
        name: "predict",
        component: predictionView
    }
]

const router = createRouter({
    history: createWebHistory('/'),
    routes
})

export default router