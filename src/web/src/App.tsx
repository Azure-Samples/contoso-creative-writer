import './app.css';
import { version } from "./version";
import Toolbar from "./components/toolbar";
import Article from "./components/article";
import Task from './components/task';

function App() {
  return (
    <main className="p-12">
      
      <div className="text-center text-3xl mt-8">Welcome to the Contoso Creative Writer</div>
      <br></br>
      <hr className="border-2 border-zinc-300" />
      <br></br>
      <span className="text-center text-1xl mt-8 ">This tool will help you write articles for the Contoso blog. Enter the required information and then click "Start Work". To watch the steps in the agent workflow complete, select the debug button in the button corner of the screen. The result will begin writing once the agent completed the tasks to write the article.</span>
      <br></br>
      <Task />
      <hr className="border-2 border-zinc-300" />
      <div className="text-center text-2xl mt-8">Article Result</div>
      <Article />
      <Toolbar />
      <div className="fixed right-0 bottom-0 mr-12 mb-2 text-zinc-300">
        {version}
      </div>
    </main>
  );
}

export default App;
