#!/bin/sh
awk '
BEGIN { 
    FS=";";  
}
{   if ( $1== "\"SIREN\"") {
        print $0
    }
    if ( $25 == "\"93\"" ) {
		print $0 ;
	}
}
END	{} 
'