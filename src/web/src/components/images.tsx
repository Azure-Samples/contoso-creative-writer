import { getUploadLocation } from "../constants"; 
import { useEffect, useState } from "react";


export const Images = () => {
  const [location, setLocation] = useState<string>("");

  useEffect(() => {
      // Fetch the upload location when the component mounts
      setLocation(getUploadLocation());
  }, []);

  console.log(location)

  return (
      <div>
          {location && <img src={location} alt="blog image" />}
      </div>
  );
};


// export const Images = () => {
//     const messages = useAppSelector((state) => state.message);
  
//     return (
//         <>
          
//           {/* image section */}
//             <div>
//               {messages.filter((message) => message.type == "designer").map((message, i) => (
//                 <div key={`message_${i}`}>
//                   <div
//                   >
//                     <div
//                     >
//                       { <img src={location} alt="blog image"/>}
//                     </div>
//                   </div>
//                 </div>
//               ))}
//             </div>
//         </>
//       );
//     };
    
    export default Images;
    