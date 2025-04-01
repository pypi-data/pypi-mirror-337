import { NotebookPanel } from '@jupyterlab/notebook';
import { KernelMessage } from '@jupyterlab/services';

interface GPUAnalysisResponse {
  has_resource_usage: boolean;
  operations: {
    compute: string[];
    memory: string[];
    transfer: string[];
    query: string[];
  };
  device_variables: string[];
  error?: string;
}

// Function to detect GPU usage in code using the gpu_check service
export const detectGPUUsage = async (notebook: NotebookPanel, code: string): Promise<boolean> => {
  console.log('Analyzing code for GPU usage with gpu_check service...');
  
  const analysisCode = `
import json
import requests

try:
    response = requests.post('http://localhost:8005/analyze', 
        json={'code': '''${code}'''}, 
        headers={'Content-Type': 'application/json'}
    )
    result = response.json()
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e), "has_resource_usage": False}))
`;

  const session = notebook.sessionContext.session;
  if (!session?.kernel) {
    return false;
  }

  try {
    let output = '';
    const future = session.kernel.requestExecute({ code: analysisCode });
    
    future.onIOPub = (msg) => {
      if (KernelMessage.isStreamMsg(msg) && msg.content.name === 'stdout') {
        output = msg.content.text;
      }
    };

    await future.done;
    const result: GPUAnalysisResponse = JSON.parse(output);
    
    console.log('GPU Analysis Result:', result);
    return result.has_resource_usage;
  } catch (error) {
    console.error('Error during GPU analysis:', error);
    return false;
  }
}; 