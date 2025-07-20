import { useEffect, useState } from 'react';

const electron = window.electron;

function App() {
  const [filePath, setFilePath] = useState(null);

  useEffect(() => {
    electron?.logSomething?.((data) => console.log(data));
  }, []);

  const handleUpload = async () => {
    if (!electron?.fileUpload) {
      alert('File dialog API not available.');
      return;
    }

    try {
      const selectedFilePath = await electron.fileUpload('openFileDialog');

      if (selectedFilePath) {
        setFilePath(selectedFilePath);
        console.log('Selected file:', selectedFilePath);
        alert(`Selected file: ${selectedFilePath}`);
        try {
          console.log(selectedFilePath);
          await electron?.processAudio(selectedFilePath);
        } catch (err) {
          alert('Error processing wav file: ' + err);
        }
      } else {
        alert('No file selected.');
      }
    } catch (error) {
      console.error('Error during file upload:', error);
      alert('An error occurred while uploading the file.');
    }
  };

  return (
    <>
      <div>
        <button onClick={handleUpload}> Upload file</button>
        {filePath && <p>Uploaded: {filePath}</p>}
      </div>
    </>
  );
}

export default App;
