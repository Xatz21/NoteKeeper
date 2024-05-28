function del_note(noteId) {
  fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => {
      if (response.ok) {
          // Remove the note from the DOM
          document.getElementById(`note_${noteId}`).remove();
      } else {
          console.error('Failed to delete note');
      }
  })
  .catch(error => {
      console.error('Error deleting note:', error);
  });
}
