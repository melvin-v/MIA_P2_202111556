import {BrowserRouter, Route, Routes} from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import ViewReports from './pages/ViewReports';
function App() {
  return (
    <BrowserRouter>
        <Routes>

          <Route path="/" element={<Home/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/view-reports" element={<ViewReports/>} />
          
        </Routes>
    </BrowserRouter>
  )
}

export default App
