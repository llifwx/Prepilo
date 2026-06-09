# Prepilo Frontend

Frontend workspace for Prepilo MVP V1.

## Stack

- Yarn
- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Axios

## Setup

Run all frontend commands from `frontend/`.

```bash
cd frontend
yarn install
```

After install, commit the generated `yarn.lock` with frontend changes.

## Environment

Create `.env.local` when the frontend app needs to call the backend:

```env
VITE_API_URL=http://127.0.0.1:8000
```

## Run

Start the backend first, then run:

```bash
yarn dev
```

Default Vite URL:

```text
http://127.0.0.1:5173
```

## Build And Checks

```bash
yarn lint
yarn build
```

The folder currently contains the dependency manifest and frontend README only. Scaffold the Vite app files in this same `frontend/` directory before running `yarn dev`.
