import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div className='page'>
      <nav className='navbar-orga'>
        <img src="src/img/mina-terrestre.png" alt="" className='logo'/>
        <h2>BUSCAMINAS</h2>
      </nav>
      <div className='txts'>
        <textarea name="console" id="" className='txt-confi'>
        </textarea>
        <div className='btns'>
          <button className='btn-confi'>Configurar</button>
          <div class="page_img">
            <a href="tu-enlace.html" class="image-link">
              <img src="src/img/tocar.png" alt="" className='imagebtn'/>
            </a>
            <a href="tu-enlace.html" class="image-link">
              <img src="src/img/close_1828527.png" alt="" className='imagebtn'/>
            </a>
          </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
