# React.js Overview

## What is React?

React (also known as React.js or ReactJS) is a free and open-source front-end JavaScript library for building user interfaces based on components. It was created by Jordan Walke, a software engineer at Meta and is maintained by Meta and a community of developers.

React was first deployed in Facebook's News Feed in 2011 and later on Instagram in 2012. It was released to the public as an open-source project in 2013.

## Core Concepts

### Components

Components are the building blocks of React applications:
- **Function Components**: Modern, recommended approach using hooks
- **Class Components**: Legacy approach (still supported)

```jsx
// Function Component
function Greeting({ name }) {
    return <h1>Hello, {name}!</h1>;
}
```

### JSX (JavaScript XML)

JSX is a syntax extension that allows HTML-like code in JavaScript:

```jsx
const element = (
    <div className="container">
        <h1>Hello World</h1>
        <p>This is JSX</p>
    </div>
);
```

### Props

Props are read-only data passed from parent to child components:

```jsx
function Button({ label, onClick, disabled = false }) {
    return (
        <button onClick={onClick} disabled={disabled}>
            {label}
        </button>
    );
}
```

### State

State is mutable data managed within a component:

```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
}
```

## React Hooks

Hooks allow function components to use state and lifecycle features:

### useState
```jsx
const [state, setState] = useState(initialValue);
```

### useEffect
```jsx
useEffect(() => {
    // Side effects: data fetching, subscriptions
    fetchData();
    
    return () => {
        // Cleanup function
    };
}, [dependency]); // Runs when dependency changes
```

### useContext
```jsx
const theme = useContext(ThemeContext);
```

### useReducer
```jsx
const [state, dispatch] = useReducer(reducer, initialState);
```

### useMemo and useCallback
```jsx
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

### useRef
```jsx
const inputRef = useRef(null);
// Access: inputRef.current.focus()
```

### Custom Hooks
```jsx
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetch(url)
            .then(res => res.json())
            .then(data => {
                setData(data);
                setLoading(false);
            });
    }, [url]);
    
    return { data, loading };
}
```

## Component Communication

### Parent to Child: Props
```jsx
<Child data={parentData} />
```

### Child to Parent: Callback Props
```jsx
<Child onUpdate={handleUpdate} />
```

### Context API: Global State
```jsx
const AppContext = createContext();

function App() {
    return (
        <AppContext.Provider value={sharedData}>
            <ChildComponent />
        </AppContext.Provider>
    );
}
```

## State Management Libraries

- **Context API + useReducer**: Built-in, great for medium apps
- **Zustand**: Lightweight and simple
- **Redux Toolkit**: Robust for large applications
- **Jotai**: Atomic state management
- **Recoil**: Facebook's experimental state library

## React Router

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
            </nav>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/users/:id" element={<UserDetail />} />
            </Routes>
        </BrowserRouter>
    );
}
```

## Popular React Ecosystem

- **Vite**: Fast build tool and dev server
- **Next.js**: Full-stack React framework
- **React Query / TanStack Query**: Data fetching and caching
- **Axios**: HTTP client
- **React Hook Form**: Form management
- **Shadcn/ui, Chakra UI, MUI**: Component libraries
- **Framer Motion**: Animation library
- **React Testing Library**: Testing utilities
