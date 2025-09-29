import React, {useState} from 'react'
import axios from 'axios'

export default function App(){
  const [file, setFile] = useState(null)
  const [log, setLog] = useState([])
  const [question, setQuestion] = useState("")
  const [response, setResponse] = useState(null)

  async function upload(){
    if(!file) return alert("choose an excel file")
    const fd = new FormData()
    fd.append('file', file)
    const res = await axios.post('http://localhost:8000/upload', fd, { headers: {'Content-Type':'multipart/form-data'}})
    setLog(l=>[...l, JSON.stringify(res.data)])
  }

  async function ask(){
    if(!question) return
    const res = await axios.post('http://localhost:8000/nlq', {question})
    setResponse(res.data)
  }

  return (
    <div style={{padding:20, fontFamily:'Arial'}}>
      <h2>AI Data Agent (Demo)</h2>
      <div>
        <input type="file" accept=".xls,.xlsx" onChange={e=>setFile(e.target.files[0])} />
        <button onClick={upload}>Upload</button>
      </div>

      <hr/>

      <div>
        <input value={question} onChange={e=>setQuestion(e.target.value)} style={{width:'60%'}} placeholder="Ask: list tables, show columns from sheet1, sum of sales group by region from sheet1" />
        <button onClick={ask}>Ask</button>
      </div>

      <pre style={{background:'#f7f7f7', padding:10}}>{JSON.stringify(response, null, 2)}</pre>

      <hr/>
      <h4>Backend logs</h4>
      <div style={{whiteSpace:'pre-wrap'}}>{log.map((l,i)=><div key={i}>{l}</div>)}</div>
    </div>
  )
}
