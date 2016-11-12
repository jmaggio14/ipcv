"""
22x17pixelz
"""
import ipcv
import numpy as np
def character_recognition(src, templates, codes,
                            threshold, filterType='spatial',
                            debug = False):

    characterCount = dict.fromkeys( codes, 0 )
    # print(templates)
    characters = dict( zip(codes,templates) )
    templateDims = (templates[0,:,:].shape[0], templates[0,:,:].shape[1])

    if filterType in ["matching","m","match","matched"]:
        img = src.flatten()
        blockLength = templateDims[0] * templateDims[1]
        for character in characters:
        	for blockIndex in range(img.size - blockLength):
	            char = characters[character].flatten()
	            block = img[blockIndex:blockIndex+blockLength]
	            similarity = np.sum(char == block) / block.size

	            if similarity >= threshold:
	                characterCount[character] = characterCount[character] + 1

    print(characterCount)

    return "test","test"
    #     templateSize = templates[0].size
    #     img = src.reshape(templateSize,1,templateSize.shape[2])
    #     templates = templates.reshape(templateSize,1,templates.shape[2])
    #     sectionIndex = 0

    #     for section in range( img.shape[2] ):
    #         section 
        
    #         for letter in range(0,src.size,templateSize):
    #             endIndex = letter+templateSize
    #             correlation = ( img[letter:endIndex] == template )
    #             similarity = np.sum(correlation) / correlation.size
    #             if similarity == 1.0:
    #                 print("match found")
                    

    #         sectionIndex +=




if __name__ == '__main__':

    import cv2
    import fnmatch
    import numpy
    import os
    import os.path

    home = os.path.expanduser('~')
    baseDirectory = home + os.path.sep + 'src/python/examples/data'
    baseDirectory += os.path.sep + 'character_recognition'

    documentFilename = baseDirectory + '/notAntiAliased/text.tif'
    documentFilename = baseDirectory + '/notAntiAliased/alphabet.tif'
    charactersDirectory = baseDirectory + '/notAntiAliased/characters'

    document = cv2.imread(documentFilename, cv2.IMREAD_UNCHANGED)

    characterImages = []
    characterCodes = []
    for root, dirnames, filenames in os.walk(charactersDirectory):
        for filename in sorted(filenames):
            currentCharacter = cv2.imread(root + os.path.sep + filename,
            cv2.IMREAD_UNCHANGED)
            characterImages.append(currentCharacter)
            code = int(os.path.splitext(os.path.basename(filename))[0])
            characterCodes.append(code)
    characterImages = numpy.asarray(characterImages)
    characterCodes = numpy.asarray(characterCodes)

    # Define the filter threshold
    # threshold = ...

    # text, histogram = character_recognition(document, 
    # characterImages, 
    # characterCodes, 
    # threshold, 
    # filterType='spatial')

    # Display the results to the user
    # .
    # .
    # .

    threshold = .78
    text, histogram = character_recognition(document, 
    characterImages, 
    characterCodes, 
    threshold, 
    filterType='matched')

    # # Display the results to the user
    # .
    # .
    # .
