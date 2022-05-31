/* 
A function to listens for changes in the file input, 
once the document has loaded, and starts the upload process.

The function also determines the file object to be uploaded. 
If one has been selected properly, it proceeds to call a function to obtain a signed POST request for the file. 
*/

(function() {
    document.getElementById('image').onchange = function(){
        var files = document.getElementById("image").files;
        var file = files[0];
        if(!file){
            return alert("No file selected.");
        }
        getSignedRequest(file);
    };
})();


/*
a function that accepts the file object and retrieves an appropriate signed request for it from the app.

The function passes the file’s name and mime type as parameters to the GET request 
since these are needed in the construction of the signed request. 

If the retrieval of the signed request was successful, 
the function continues by calling a function to upload the actual file:
 */
function getSignedRequest(file){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/sign_s3?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                uploadFile(file, response.data, response.url);
            }
            else{
                alert("Could no get signed URL.");
            }
        }
    };
    xhr.send();
}

/*
This function accepts the file to be uploaded, the S3 request data, 
and the URL representing the eventual location of the avatar image. 
The latter two arguments will be returned as part of the response from the app. 
The function, if the request is successful, updates the preview element to the new 
avatar image and stores the URL in the hidden input so that it can be submitted 
for storage in the app.

Now, once the user has completed the rest of the form and clicked Submit, 
the name, username, and avatar image can all be posted to the same endpoint.
 */
function uploadFile(file, s3Data, url){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', s3Data.url);

    var postData = new FormData();
    for(key in s3Data.fields){
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);

    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4){
            if(xhr.status === 200 || xhr.status === 204){
                document.getElementById('preview').src = url;
                document.getElementById('avatar-url').value = url;
            }
            else{
                alert("Could not upload file.");
            }
        }
    };
    xhr.send(postData);
}
