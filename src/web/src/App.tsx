import './app.css';
import { version } from "./version";
import Toolbar from "./components/toolbar";
import Article from "./components/article";
import Task from './components/task';

function App() {
  return (
    <main className="p-8 flex flex-col min-h-screen">
      {/* Header Section */}
      <header className="text-center my-6">
        <h1 className="text-4xl font-bold text-gray-800">Contoso Creative Writer</h1>
        <p className="text-xl text-gray-600 mt-2">
          This tool helps you write articles for the Contoso blog.
          
        </p>
        <hr className="border-2 border-gray-300 my-6" />
      </header>

      {/* Main Content Wrapper */}
      <div className="flex flex-col lg:flex-row lg:space-x-8 mt-8">
        {/* Task Section - Left Aligned */}
        <div className="lg:w-1/3 bg-gray-100 p-6 rounded shadow-md">
          <h3 className="text-2xl text-gray-800 mb-4">Create Your Article</h3>
          <Task />
          <div className="text-center mt-4">
            <Toolbar />
          </div>
        </div>

        {/* Article Section - Right Aligned */}
        <section className="lg:w-2/3 flex-grow mt-8 lg:mt-0">
          <div className="bg-white shadow-md rounded p-6">
            <h2 className="text-3xl text-gray-800 mb-4">Your Article</h2>
            <Article />
          </div>
        </section>
      </div>

      {/* Version Number */}
      <div className="fixed right-0 bottom-0 mr-6 mb-2 text-gray-400">
        {version}
      </div>
    </main>
  );
}

export default App;


