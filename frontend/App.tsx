import { S3Client } from '@aws-sdk/client-s3';
import { Upload } from '@aws-sdk/lib-storage';
import { Credentials } from 'aws-sdk';
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
  const upload = async () => {
    const creds = new Credentials(
      import.meta.env.VITE_AWS_AccessID,
      import.meta.env.VITE_AWS_SecretKey
    );
    const parallelUploads3 = new Upload({
      client: new S3Client({ region: 'ap-northeast-1', credentials: creds }),
      params: { Bucket: 'image-converter-image-storage-s3-bucket', Key: file?.name, Body: file },
      leavePartsOnError: false,
    });
    parallelUploads3.on('httpUploadProgress', (progress) => {
      console.log(progress);
    });

    await parallelUploads3.done();
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
          <button type="button" disabled={!file && true} onClick={upload}>
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
