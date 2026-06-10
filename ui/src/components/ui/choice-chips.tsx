import * as React from "react"

import { cn } from "@/lib/utils"

interface ChoiceChipsProps {
    options: {
        value: string;
        label: string;
    }[];
    value: string;
    onChange: (value: string) => void;
    className?: string;
}

export function ChoiceChips({ options, value, onChange, className }: ChoiceChipsProps) {
    return (
        <div className={cn("flex gap-2 p-4", className)}>
            {options.map((option) => (
                <button
                    key={option.value}
                    onClick={() => onChange(option.value)}
                    className={cn(
                        "px-4 py-2 rounded-full text-sm font-medium transition-all",
                        value === option.value
                            ? "bg-primary text-primary-foreground"
                            : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                    )}
                >
                    {option.label}
                </button>
            ))}
        </div>
    )
}
