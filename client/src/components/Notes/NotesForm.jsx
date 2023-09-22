import { useState } from 'react'

function NotesForm({ createNote }) {

  const [content, setContent] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    createNote(content)
    setContent('')
  }

  const handleChangeContent = e => setContent(e.target.value)

  return (
    <form onSubmit={handleSubmit}>

      <h3>New Note:</h3>

      <input
        type="text"
        onChange={handleChangeContent}
        value={content}
      />

      <input type="submit" value={'Add Note'} />

    </form>
  )

}

export default NotesForm
