import { useEffect, useState } from 'react';
import reactLogo from './assets/react.svg';
import './App.css';

const electron = window.electron;

function App() {
  const [count, setCount] = useState(0);
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
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <div>
        <button onClick={handleUpload}> Upload file</button>
        {filePath && <p>Uploaded: {filePath}</p>}
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
