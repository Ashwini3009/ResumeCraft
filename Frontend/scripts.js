// $(document).ready(function() {
//     $('#resumeForm').on('submit', function(event) {
//         event.preventDefault();

//         var formData = new FormData(this);
//         var resumeFile = $('#resumeFile')[0].files[0];

//         if (resumeFile) {
//             $('#loading').show();
//             $('#scoreResult').hide();

//             var reader = new FileReader();
//             reader.onloadend = function() {
//                 var fileData = reader.result;
//                 // Simulate ATS analyzer response (backend interaction)
//                 analyzeResume(fileData);
//             };

//             // Read the resume file
//             reader.readAsDataURL(resumeFile);
//         }
//     });

//     // Simulated ATS analysis function
//     function analyzeResume(fileData) {
//         // Simulated delay for the backend call
//         setTimeout(function() {
//             var atsScore = Math.floor(Math.random() * 100) + 1; // Random ATS score
//             var suggestions = [
//                 'Use more action verbs.',
//                 'Include more relevant skills.',
//                 'Use standard resume formatting.'
//             ];

//             $('#loading').hide();
//             $('#atsScore').text(atsScore + '%');
//             $('#atsSuggestions').empty();

//             suggestions.forEach(function(suggestion) {
//                 $('#atsSuggestions').append('<li>' + suggestion + '</li>');
//             });

//             $('#scoreResult').show();
//         }, 2000); // Simulated backend delay (2 seconds)
//     }
// });
