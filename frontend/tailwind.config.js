import { nextui } from "@nextui-org/react"

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./layouts/**/*.{js,ts,jsx,tsx,mdx}",
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {},
    },
    darkMode: "class",
    plugins: [
        nextui({
            themes: {
                light: {
                    colors: {
                        background: "#ECEDEE",
                        foreground: "#11181C",
                        primary: {
                            foreground: "#FFFFFF",
                            DEFAULT: "#006FEE",
                        },
                    },
                },
                dark: {
                    colors: {
                        background: "#1D1D1D",
                        foreground: "#ECEDEE",
                        primary: {
                            foreground: "#FFFFFF",
                            DEFAULT: "#006FEE",
                        },
                    },
                },
            },
        }),
    ],
}
