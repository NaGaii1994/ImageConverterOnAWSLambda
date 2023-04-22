import { ChangeEvent, useRef, useState } from 'react';
import './App.css';

function App() {
  const inputFileReference = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | undefined>();
  const onChangeFile = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };
  return (
    <div className="App">
      <h1>Image Converter To WebP</h1>
      <div className="card">
        <form method="post" encType="multipart/form-data">
          <input
            onChange={onChangeFile}
            ref={inputFileReference}
            style={{ display: 'none' }}
            type="file"
            id="imageInput"
            name="imageInput"
            accept="image/png, image/jpeg, image/bmp, image/gif"
          />
          <button type="button" onClick={() => inputFileReference.current?.click()}>
            {file ? 'Change Image' : 'Select Image'}
          </button>
          <button type="button" disabled={!file && true}>
            Upload Image
          </button>

          {file ? (
            <p>
              You Select <code>{file?.name}</code> File
            </p>
          ) : (
            <p>Please Select file.</p>
          )}
        </form>
      </div>
      <p className="read-the-docs">This application convert a image you upload to webp.</p>
    </div>
  );
}

export default App;
