import { useState } from 'react'
import './App.css'

function App() {
  const [respuesta, setRespuesta] = useState(null)

  const enviarAnalizador = async () => {
    const textarea = document.querySelector(".txt-confi")
    const texto = textarea.value

    try {
      const response = await fetch("http://localhost:4000/manual", {
        method: "POST",
        headers: {
          "Content-Type": "text/plain",
        },
        body: texto,
      })

      const data = await response.json()
      console.log("Respuesta analizador:", data)
      setRespuesta(data.message || 'Configuración enviada.')
    } catch (error) {
      console.error("Error al enviar al analizador:", error)
      setRespuesta("Error al conectar con el backend.")
    }
  }

  return (
    <>
      <div className='page'>
        <nav className='navbar-orga'>
          <img src="src/img/mina-terrestre.png" alt="" className='logo' />
          <h2>BUSCAMINAS</h2>
        </nav>

        <div className='txts'>
          <textarea name="console" className='txt-confi'></textarea>

          <div className='btns'>
            <button className='btn-confi' onClick={enviarAnalizador}>Configurar</button>

            <div className="page_img">
              <a href="#" className="image-link">
                <img src="src/img/tocar.png" alt="" className='imagebtn' />
              </a>
              <a href="#" className="image-link">
                <img src="src/img/close_1828527.png" alt="" className='imagebtn' />
              </a>
            </div>
          </div>

          {respuesta && <div className="respuesta">{respuesta}</div>}
        </div>
      </div>
    </>
  )
}

export default App
