import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import AppLayout from './layouts/AppLayout'
import TeacherWorkbenchPage from './pages/TeacherWorkbenchPage'
import ClassroomPage from './pages/ClassroomPage'
import StudentPage from './pages/StudentPage'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<TeacherWorkbenchPage />} />
          <Route path="/classroom" element={<ClassroomPage />} />
          <Route path="/classroom/:convId" element={<ClassroomPage />} />
          <Route path="/student/:demoId" element={<StudentPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
