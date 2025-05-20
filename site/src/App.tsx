import Home from './pages/Homepage';
import GameSelector from './pages/GameSelector'
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/games" element={<GameSelector />} />
      <Route path="/game/:gameId" element={<Home />} />
    </Routes>
  );
}

export default App;
