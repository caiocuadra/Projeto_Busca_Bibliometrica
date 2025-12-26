import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Necessário para o Docker mapear a porta
    strictPort: true,
    allowedHosts: [    // <--- A CORREÇÃO ESTÁ AQUI
      'nlp.naturaldobem.com.br',
      'localhost',
      '127.0.0.1'
    ],
    port: 5173, 
    watch: {
      usePolling: true, // CRUCIAL: Faz o container "sentir" as mudanças nos arquivos do Windows/Linux
    }
  }
})