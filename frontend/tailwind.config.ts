import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#050a18", // Darker for high contrast text
          900: "#0b132b",
          700: "#1c2541",
          500: "#3a506b",
          400: "#5bc0be", // Adjusted for better visibility
          300: "#8cdcd9", // Lighter accent
          100: "#e0fbfc",
          50: "#f0faff", // Very light background
        },
        sand: {
          50: "#f9f7f3",
          100: "#f2eee5",
          200: "#e4d8c9",
          300: "#d6c6b0", // Darker border
        },
        accent: {
          DEFAULT: "#ff7f50",
          hover: "#e66a3c", // Darker hover state
        },
        surface: {
          white: "#ffffff",
          subtle: "#f8fafc",
        }
      },
      fontFamily: {
        sans: ["var(--font-space-grotesk)", "sans-serif"], // Use CSS variable
        mono: ["var(--font-jetbrains-mono)", "monospace"],
      },
      boxShadow: {
        card: "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
        "card-hover": "0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025)",
      },
    },
  },
  plugins: [],
};

export default config;
