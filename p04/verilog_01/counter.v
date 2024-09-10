`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company  :   Fundación Fulgor
// Engineer :   Martinez Luciano
// Porject  :   Trabajo Partico N°4
// Module   :   Contador ==> "counter"
//////////////////////////////////////////////////////////////////////////////////

module counter  
    /* parametrización */
    #(
        parameter n_SW          = 3             ,   // cantidad de bits del selector
        parameter n_COUNT       = 32                // cantidad de bits del contador
    )
    /* entradas y salidas del modulo */
    (
        input                   i_clk           ,   // entrada de clock 
        input                   i_reset         ,   // entrada de reset
        input   [n_SW -1 : 0]   i_sw            ,   // entrada de selectores <para el limit_ref del contador>
        output                  o_valid             // salida de valid para el SR y/o FS
    );


    /* localparam: define una constante de solo lectura dentro del modulo */
    localparam R0 = (2 ** (n_COUNT -10)) -1     ;   // const: R0 = 4,194,303
    localparam R1 = (2 ** (n_COUNT -11)) -1     ;   // const: R1 = 2,097,151
    localparam R2 = (2 ** (n_COUNT -12)) -1     ;   // const: R2 = 1,048,575
    localparam R3 = (2 ** (n_COUNT -13)) -1     ;   // const: R3 = 524,287     
    

    /* reg: permite almacenar valores en bloques secuenciales y combinacionales <always> */
    reg         [n_COUNT-1 : 0] counter         ;   // contador
    reg                         enable          ;   // enable to (shift) SR or (flash) FS


    /* wire: para conecta señales dentro de un módulo */
    wire        [n_COUNT-1 : 0] limit_ref       ;   // limite de referencia


    // asignación del valor de limite de referencia
    assign limit_ref =  (i_sw[2:1] == 2'b00) ? R0 :
                        (i_sw[2:1] == 2'b01) ? R1 :
                        (i_sw[2:1] == 2'b10) ? R2 : R3;


    /* always secuencial <estructura del contador>: lista sencible => señales asincronas de clock y reset */
    always @(posedge i_clk or posedge i_reset) begin
        
        // para: reset
        if (i_reset == 1'b1) begin
            counter     <= {n_COUNT {1'b0}} ;   // reinicio del contador
            enable      <= 1'b0             ;   // la salida de enable to shift permanece en 0    
        end

        // para i_sw[0] = 1 : habilitador del contador
        else if (i_sw[0] == 1'b1) begin
            
            // para:
            if(counter < limit_ref) begin
                counter <= counter +1       ;   // se incrementa el contador
                enable  <= 1'b0             ;   // la salida de enable to shift permanece en 0
            end 

            // si se supera el limite de referencia
            else begin
                counter <= {n_COUNT{1'b0}}  ;   // se reinicia el contador
                enable  <= 1'b1             ;   // se envia un 1 en enable to shift
            end
        end
    end

    // asignación de la señal de enable to shift a la salida de "valid"
    assign o_valid  = enable ;  

endmodule
