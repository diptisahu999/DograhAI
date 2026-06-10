import { Loader2 } from "lucide-react";

export default function SpinLoader(){
    return(
        <div className="flex items-center justify-center min-h-screen">
                <Loader2 className="w-15 h-15 animate-spin" />
              </div>
    )
}
