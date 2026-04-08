/// <reference types="vite/client" />

// src/env.d.ts

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  // On définit que chaque fichier .vue exporte un composant typé
  const component: DefineComponent<{}, {}, any>;
  export default component;
}