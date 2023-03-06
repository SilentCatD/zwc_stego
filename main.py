from stego import embed, extract

embed('msg.txt', 'cover.txt')
extract('cover_embedded.txt')