import { useRef, useState } from 'react'
import axios from 'axios'

import './App.css'

function App() {
  const [text, setText] = useState('')
  const fileInputRef = useRef(null) // Referencia al input de archivo

  // Enviar texto plano a /analizer
  const handleConfigurar = async () => {
    try {
      const response = await axios.post('http://localhost:4000/analizer', text, {
        headers: { 'Content-Type': 'text/plain' }
      })
      console.log(response.data)
      alert("✔️ Texto enviado correctamente")
    } catch (error) {
      console.error("❌ Error al enviar texto:", error)
    }
  }

  // Enviar comando JSON a /manual
  const enviarComandoManual = async (comando) => {
    try {
      const response = await axios.post('http://localhost:4000/manual', {
        mensaje: comando
      })
      console.log(response.data)
      alert(`✔️ Comando "${comando}" enviado`)
    } catch (error) {
      console.error("❌ Error al enviar comando:", error)
    }
  }

  // Abrir explorador y cargar contenido del archivo
  const handleArchivo = (event) => {
    const file = event.target.files[0]
    if (file && file.name.endsWith('.org')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setText(e.target.result)
      }
      reader.readAsText(file)
    } else {
      alert("⚠️ Selecciona un archivo .org válido")
    }
  }

  // Activar input oculto al hacer clic en la imagen
  const abrirExplorador = () => {
    fileInputRef.current.click()
  }

  return (
    <>
      <div className='page'>
        <nav className='navbar-orga'>
          <img src="src/img/mina-terrestre.png" alt="" className='logo' />
          <h2>BUSCAMINAS</h2>
        </nav>
        <div className='txts'>
          <textarea
            name="console"
            className='txt-confi'
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className='btns'>
            <button className='btn-confi' onClick={handleConfigurar}>Configurar</button>
            <div className="page_img">
              <a onClick={() => enviarComandoManual("initJuego")} className="image-link">
                <img src="src/img/tocar.png" alt="" className='imagebtn' />
              </a>
              <a onClick={() => enviarComandoManual("finJuego")} className="image-link">
                <img src="src/img/close_1828527.png" alt="" className='imagebtn' />
              </a>
              <a onClick={abrirExplorador} className="image-link">
                <img src="src/img/open.png" alt="" className='imagebtn' />
              </a>
              <input
                type="file"
                accept=".org"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleArchivo}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
