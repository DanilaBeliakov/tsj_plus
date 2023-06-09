const fileUploader = document.getElementById('file-uploader');

fileUploader.addEventListener('change', (event) => {
  const files = event.target.files;
  console.log('files', files);
  
  for (const file of files) {
    const name = file.name;
    const type = file.type ? file.type : 'NA';
    const size = file.size;
    const lastModified = file.lastModified;
    console.log({file, name, type, size, lastModified});
    
    const feedback = document.getElementById('feedback');
    const msg = ` File Name: ${name} <br/>
              File Size: ${size} <br/>
              File type: ${type} <br/>
              File Last Modified: ${new Date(lastModified)}`;
              
    feedback.innerHTML = msg;
  }
});