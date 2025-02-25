	.model tiny
	.code

	locals @@

	org 100h
				ADDR_OF_VIDEO_MEMORY    equ 0b800h
				ADDR_OF_COMMAND_STR     equ 082h
				SYSTEM_CALL             equ 21h
				RETURN_0                equ 4c00h

    Start:
				jmp main
                String db "Enter the password: $"

    main:	
				mov ah, 09h                      ; 
				mov dx, offset String		     ; printf ("%s", &String)
				int SYSTEM_CALL                  ; 

                call getPwd

                call exit_0

;--------------------------------------------------------------------------------------------------
 	; ENTRY:   None
 	; EXIT:    
 	; DESTROY: si
 	getPwd 		proc

 				

 				
 				ret
    endp
;--------------------------------------------------------------------------------------------------
   


;--------------------------------------------------------------------------------------------------
 	exit_0 		proc
 				mov ax, RETURN_0
 				int SYSTEM_CALL
 				ret
 	endp
;--------------------------------------------------------------------------------------------------

	end Start