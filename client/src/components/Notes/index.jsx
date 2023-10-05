import { useState, useEffect } from 'react'
import NotesForm from './NotesForm'

const POST_HEADERS = {
  'Content-Type': 'application/json',
  'Accepts': 'application/json'
}

const URL = "/api/v1"

function Notes() {

  // STATE //

  const [notes, setNotes] = useState([])

  // EFFECTS //

  useEffect(() => {
    fetch(URL + '/notes')
    .then(res => {
      if (res.ok) {
        res.json()
        .then(data => setNotes(data))
      }
    })
    .catch(e => console.log(e))
  }, [])

  // EVENTS //

  async function createNote(content) {
    const res = await fetch(URL + '/notes', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify({content})
    })
    if (res.ok) {
      const newNote = await res.json()
      setNotes([...notes, newNote])
    }
  }

  // RENDER //

  return (

    <div>

      { notes.map(note => <h3>{note.id} {note.content}</h3>) }

      <NotesForm createNote={createNote} />

    </div>

  )

}

export default Notes
