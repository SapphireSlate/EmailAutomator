# Email Automator Frontend

A modern, responsive frontend for the Email Automator system built with Next.js 14, TypeScript, Tailwind CSS, and Framer Motion.

## Features

- 🎨 Beautiful, responsive UI with smooth animations
- 🌓 Dark mode support
- 📊 Real-time campaign statistics
- 📧 Email template management
- 👥 Contact list management
- 📈 Campaign analytics
- ⚡ Fast and efficient performance

## Prerequisites

- Node.js 18.17 or later
- npm 9.6.7 or later

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the root directory and add your environment variables:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # Reusable UI components
│   ├── lib/             # Utility functions and hooks
│   ├── types/           # TypeScript type definitions
│   └── styles/          # Global styles and Tailwind config
├── public/              # Static assets
└── package.json         # Project dependencies and scripts
```

## Development

- `npm run dev` - Start the development server
- `npm run build` - Build the production application
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint for code quality

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
