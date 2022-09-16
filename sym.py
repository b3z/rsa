# /* secretA  215317 */
# /* secretB 215317 */
import cryptocode

passkey = str(215317)

str_encoded = cryptocode.encrypt("I am okay", passkey)

print(str_encoded)

str_decoded = cryptocode.decrypt(str_encoded, passkey)
print(str_decoded)
