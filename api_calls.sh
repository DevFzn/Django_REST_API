#!/usr/bin/env bash
#
# API Calls - curl

API_URL='http://127.0.0.1:8000'
USER="$(read -p 'Username: ' && echo ${REPLY})"
printf 'Password: '
PASS="$(read -s ; echo ${REPLY})"
TOKEN=''

while :; do
    printf '\n\nLlamadas a API en %s\n' "${API_URL}"
    read -p 'URL ok? (Y/n/q)'
    case "${REPLY}" in
        [yY]|[sS]|[Ss][Ii]|[Yy][Ee][Ss]|'')
            break
            ;;
        [Nn]|[Nn][Oo])
            API_URL="$(read -p 'URL: ' && echo ${REPLY})"
            echo
            ;;

        [Qq])
            exit 0
            ;;
        *)
            printf '\nOpción inválida [%s]\n' "${REPLY}"
            ;;
    esac
done

TOKEN="$(curl -sX POST -F "username=${USER}" -F "password=${PASS}" \
                          "${API_URL}/api-token-auth/" | jq -r .'[]')"
ITEM_ID="$(curl -sX GET -H "Authorization: Token ${TOKEN}" "${API_URL}/item/" |
            jq -r '.data[-1].id')"
ORDER_ID="$(curl -sX GET -H "Authorization: Token ${TOKEN}" "${API_URL}/order/" |
            jq -r '.data[-1].id')"

separator(){
    echo && printf '┄%.0s' {1..85} && echo
}

api_get_token(){
    separator && printf '%s\n' "${1}"
    printf 'curl -X POST -F "username=%s" -F "password=%s" "%s/api-token-auth/"\n' \
           "${USER}" "XXXXXXXX"
    curl -sX POST -F "username=${USER}" -F "password=${PASS}" \
                       "${API_URL}/api-token-auth/" | jq
}

api_item_call(){
    separator 
    printf '%s\n' "${1}"
    printf 'curl -X GET -H "Authorization: Token %s"\n\t\t\b"%s/%s"\n' "${TOKEN}" \
           "${API_URL}" "${2}"
    curl -sX GET -H "Authorization: Token ${TOKEN}" "${API_URL}/${2}" | jq
}

api_order_call(){
    separator 
    printf '%s\n' "${1}"
    printf 'curl -X POST -H "Content-Type: application/json" \ \n'
    printf '     -H "Authorization: Token %s" \ \n' "${TOKEN}"
    printf '     -d "{"item": "%s", "quantity": "%s"} \ \n' "${3}" "${4}"
    printf '     %s/order/\n' "${API_URL}"
    curl -sX POST -H 'Content-Type: application/json' \
                  -H "Authorization: Token ${TOKEN}" \
                  -d "{\"item\": \"${ITEM_ID}\", \"quantity\": \"${4}\"}" \
                  "${API_URL}/${2}" | jq
}

api_getorder_call(){
    separator 
    printf '%s\n' "${1}"
    printf 'curl -X GET -H "Authorization: Token %s"\n    %s/%s' \
           "${TOKEN}" "${API_URL}" "${2}"
    curl -sX GET -H "Authorization: Token ${TOKEN}" "${API_URL}/${2}" | jq
}

api_contact_call(){
    separator 
    printf '%s\n' "${1}"
    printf 'curl -X POST -H "Content-type: application/json" \ \n'
    printf '     -d "{"name": "%s", "message": "%s", "email":"%s"}"\n' \
           "${2}" "${3}" "${4}"
    printf '     %s/contact/\n' "${API_URL}"
    curl -sX POST -H "Content-type: application/json" \
         -d "{\"name\": \"${2}\", \"message\": \"${3}\", \"email\":\"${4}\"}" \
         "${API_URL}/contact/" | jq
}

api_get_token "1) Devuelve el token"
api_item_call "2) Devuelve todos los items" "item/"
api_item_call "3) Devuelve el primer item" "item/${ITEM_ID}/"
api_order_call "4) Realiza un pedido" "order/" "${ITEM_ID}" 1
api_getorder_call "5) Devuelve todas las ordenes" "order/"
api_getorder_call "6) Devuelve la primera orden" "order/${ORDER_ID}/"
api_contact_call "7) Crea un contacto" "DevFzn" "test contacto" "devfzn@mail.com"

exit 0
