import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import AppLayout from './layouts/AppLayout'
import TeachPage from './pages/TeachPage'
import ClassroomPage from './pages/ClassroomPage'
import StudentPage from './pages/StudentPage'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<TeachPage />} />
          <Route path="/classroom" element={<ClassroomPage />} />
          <Route path="/student/:id" element={<StudentPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
