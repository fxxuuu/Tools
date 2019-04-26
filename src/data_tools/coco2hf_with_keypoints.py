import json
key_points_train_annotation_path = '/share10/public/fangxin/external_datasets/coco/annotations/annotations_trainval2017/annotations/person_keypoints_train2017.json'
key_point_image_path = 'images/train2017/train2017/'
human_format_path = '/share10/public/fangxin/external_datasets/coco/hf_annotations_v2/annotation_trainval2017.hf'
path_list_path = '/share10/public/fangxin/external_datasets/coco/hf_annotations_v2/trainval2017_pathlist.txt'

key_points_train_annotation_f = None
human_format = None
path_list = None

key_points_train_idToIndex = {}
key_points_train_annotaToindex = {}

def main():
    global key_points_train_annotation_f, human_format, path_list
    log = open('log.txt','w')
    try:

        log.write(str(1)+'\n')
        key_points_train_annotation_f = open(key_points_train_annotation_path, 'r')
        path_list = open(path_list_path, 'w')
        human_format = open(human_format_path, 'w')
        print(str(2)+'\n')
        key_points_train_annotation = json.loads(key_points_train_annotation_f.read())


        key_points_trian_annotation_images = key_points_train_annotation['images']
        key_points_train_annotation_annotations = key_points_train_annotation['annotations']

        # index = 0
        # for image in key_points_trian_annotation_images:
        #     if image['id'] not in key_points_train_idToIndex:
        #         key_points_train_idToIndex[image['id']] = [index]
        #     else:
        #         key_points_train_idToIndex[image['id']].append(index)
        #     index += 1

        index = 0
        for annotation in key_points_train_annotation_annotations:
            image_id = annotation['image_id']
            if image_id not in key_points_train_annotaToindex:
                key_points_train_annotaToindex[image_id] = [index]
            else:
                key_points_train_annotaToindex[image_id].append(index)
            index += 1

        print(5)
        log.write(str(5)+'\n')
        count = 0
        for image in key_points_trian_annotation_images:

            name = image['file_name']
            image_id = image['id']
            print(11)
            try:
                count += 1
                key_point_annotaion = [key_points_train_annotation_annotations[i] for i in key_points_train_annotaToindex[image_id]]
            except:
                continue
            print(12)
            print('processing,',image_id)
            log.write('processing,'+str(image_id)+'\n')
            bboxNum = len(key_point_annotaion)
            output_str = str(bboxNum)+' '
            for k in key_point_annotaion:
                bbox = k['bbox']
                x = bbox[0]
                y = bbox[1]
                w = bbox[2]
                h = bbox[3]
                output_str += str(x)+' '+str(y)+' ' + str(x+w)+' ' + str(y+h)+' '+ str(2)+' '
                keyPoints = k['keypoints']
                print(6)
                log.write(str(6) + '\n')
                '''nose point'''
                # x1 = keyPoints[0]
                # y1 = keyPoints[1]
                # v1 = keyPoints[2]
                # output_str += str(x1) + ' ' + str(y1) + ' ' #+ str(v1) + ' '

                '''left shoulder'''
                x11 = keyPoints[15]
                y11 = keyPoints[16]
                v11 = keyPoints[17]
                output_str += str(x11) + ' ' + str(y11) + ' '  # + str(v11) + ' '
                '''right shoulder'''
                x12 = keyPoints[18]
                y12 = keyPoints[19]
                v12 = keyPoints[20]
                output_str += str(x12) + ' ' + str(y12) + ' '  # + str(v12) + ' '
                print(7)
                log.write(str(7) + '\n')
                x2 = keyPoints[33]
                y2 = keyPoints[34]
                v2 = keyPoints[35]
                output_str += str(x2) + ' ' + str(y2) + ' ' #+ str(v2) + ' '
                print(8)
                log.write(str(8) + '\n')
                x3 = keyPoints[36]
                y3 = keyPoints[37]
                v3 = keyPoints[38]
                output_str += str(x3) + ' ' + str(y3) + ' ' #+ str(v3) + ' '
                print(9)

                output_str += str(v11) + ' ' + str(v12) + ' ' + str(v2) + ' ' + str(v3) + ' '
                # output_str += str(v1) + ' ' + str(v2) + ' ' + str(v3) + ' '

            log.write(str(9) + '\n')
            output_str = output_str.rstrip() + '\n'
            human_format.write(output_str)
            path_list.write(key_point_image_path+name+'\n')
            print(10)
            log.write(str(10) + '\n')
        print('Processed pics,', count)

    except Exception as e:
        global key_points_train_annotation_f, human_format, path_list
        if key_points_train_annotation_f:
            key_points_train_annotation_f.close()
        if path_list:
            path_list.close()
        if human_format:
            human_format.close()
        print('failed,', repr(e))

if '__main__'==__name__:

    main()
